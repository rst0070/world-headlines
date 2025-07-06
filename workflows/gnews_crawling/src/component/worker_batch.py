import asyncio
import logging
from typing import Callable, Optional, List, Dict, Any
import random
from copy import deepcopy


logger = logging.getLogger(__name__)


async def _create_batch_worker(
    worker_name: str,
    worker_id: int,
    worker_func: Callable[[Any, Any], Any] | Callable[[Any], Any],
    input_queue: Optional[asyncio.Queue] = None,
    input_batch_size: Optional[int] = None,
    output_queue: Optional[asyncio.Queue] = None,
    params: Optional[Any] = None,
):
    if input_queue is None:
        logger.info(
            {
                "log_type": "batch_worker_producing",
                "log_data": f"{worker_name} Worker {worker_id} is producing job",
            }
        )
        assert isinstance(output_queue, asyncio.Queue)

        result = await worker_func(params)
        if result is None:
            return

        if isinstance(result, List):
            for item in result:
                await output_queue.put(item)
        else:
            await output_queue.put(result)

        return

    logger.info(f"{worker_name} Worker {worker_id} is consuming job")
    assert isinstance(input_queue, asyncio.Queue)
    assert isinstance(input_batch_size, int)

    batch_items = []
    while True:
        item = await input_queue.get()

        # Handle termination signal
        if item is None:
            break

        try:
            retry_count = 0
            result = None

            ## Get process result
            if isinstance(item, Dict) and "_retry_metadata" in item:
                retry_count = item["_retry_metadata"]["retry_count"]
                result = await worker_func(
                    item["_retry_metadata"]["batch_items"], params
                )
                if result is None:
                    continue
            else:
                batch_items.append(item)
                if len(batch_items) >= input_batch_size:
                    result = await worker_func(batch_items, params)
                    batch_items.clear()
                    if result is None:
                        continue

            ## Put result into queue
            if output_queue and result:
                if isinstance(result, List):
                    for item in result:
                        await output_queue.put(item)
                else:
                    await output_queue.put(result)

        except Exception as e:
            if retry_count < 3:
                logger.error(
                    {
                        "log_type": "batch_worker_consuming_failed",
                        "log_data": {
                            "worker_name": worker_name,
                            "worker_id": worker_id,
                            "retry_count": retry_count,
                            "error": str(e),
                        },
                    }
                )

                backoff_time = min(60, (10**retry_count) + random.uniform(0, 1))

                if isinstance(item, Dict) and "_retry_metadata" in item:
                    retry_batch = deepcopy(item)
                    retry_batch["_retry_metadata"]["retry_count"] = retry_count + 1
                else:
                    retry_batch = {
                        "_retry_metadata": {
                            "retry_count": retry_count + 1,
                            "batch_items": batch_items,
                        }
                    }

                await asyncio.sleep(backoff_time)
                await input_queue.put(retry_batch)

            else:
                logger.error(
                    {
                        "log_type": "batch_worker_consuming_failed",
                        "log_data": {
                            "worker_name": worker_name,
                            "worker_id": worker_id,
                            "error": str(e),
                        },
                    }
                )
                raise e
        finally:
            input_queue.task_done()

    if len(batch_items) > 0:
        result = await worker_func(batch_items, params)
        if output_queue:
            if isinstance(result, List):
                for item in result:
                    await output_queue.put(item)
            else:
                await output_queue.put(result)


async def worker_batch_supervisor(
    worker_name: str,
    worker_func: Callable[[Any, Any], Any] | Callable[[Any], Any],
    num_workers: int,
    input_queue: Optional[asyncio.Queue] = None,
    input_batch_size: Optional[int] = None,
    output_queue: Optional[asyncio.Queue] = None,
    num_next_workers: Optional[int] = None,
    max_retries: int = 3,
    params: Optional[Any] = None,
):
    workers = []

    ## Init workers
    def create_workers(worker_count: int):
        """Create a list of worker tasks"""
        workers = []
        for i in range(worker_count):
            workers.append(
                asyncio.create_task(
                    _create_batch_worker(
                        worker_name,
                        i,
                        worker_func,
                        input_queue,
                        input_batch_size,
                        output_queue,
                        params,
                    )
                )
            )
        return workers
    
    workers = create_workers(num_workers)

    for retry_attempt in range(max_retries + 1):
        logger.info(
            {
                "log_type": "batch_supervisor_attempt",
                "log_data": {
                    "worker_name": worker_name,
                    "attempt": retry_attempt,
                    "total_workers": len(workers),
                },
            }
        )
        
        results = await asyncio.gather(*workers, return_exceptions=True)
        
        # find workers with exceptions
        failed_worker_indices = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(
                    {
                        "log_type": "batch_worker_failed",
                        "log_data": {
                            "worker_name": worker_name,
                            "worker_id": i,
                            "attempt": retry_attempt,
                            "error": str(result),
                        },
                    }
                )
                failed_worker_indices.append(i)
            else:
                logger.info(
                    {
                        "log_type": "batch_worker_completed",
                        "log_data": {
                            "worker_name": worker_name,
                            "worker_id": i,
                            "attempt": retry_attempt,
                        },
                    }
                )
        
        # If no failures, done
        if not failed_worker_indices:
            logger.info(
                {
                    "log_type": "batch_supervisor_completed",
                    "log_data": {
                        "worker_name": worker_name,
                        "total_attempts": retry_attempt,
                        "successful_workers": len(workers),
                    },
                }
            )
            break
            
        # raise error if max retries exceeded
        if retry_attempt >= max_retries:
            logger.error(
                {
                    "log_type": "batch_supervisor_max_retries_exceeded",
                    "log_data": {
                        "worker_name": worker_name,
                        "failed_workers": len(failed_worker_indices),
                        "max_retries": max_retries,
                    },
                }
            )
            raise Exception(f"Batch supervisor failed to complete after {max_retries} retries")
        
        # Re-create failed workers
        workers = create_workers(len(failed_worker_indices))
        logger.info(
            {
                "log_type": "batch_supervisor_recreate_workers",
                "log_data": {
                    "worker_name": worker_name,
                    "retry_attempt": retry_attempt,
                    "failed_workers": len(failed_worker_indices),
                },
            }
        )

    if output_queue:
        for _ in range(num_next_workers):
            await output_queue.put(None)
