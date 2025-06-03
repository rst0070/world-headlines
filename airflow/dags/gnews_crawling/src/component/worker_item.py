import asyncio
import logging
from typing import Callable, Optional, List, Dict, Any
import random


logger = logging.getLogger(__name__)


async def _create_worker(
    worker_name: str,
    worker_id: int,
    worker_func: Callable[[Any, Any], Any] | Callable[[Any], Any],
    input_queue: Optional[asyncio.Queue] = None,
    output_queue: Optional[asyncio.Queue] = None,
    params: Optional[Any] = None,
):
    if input_queue is None:
        logger.info(
            {
                "log_type": "item_worker_producing",
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

    else:
        logger.info(
            {
                "log_type": "item_worker_consuming",
                "log_data": f"{worker_name} Worker {worker_id} is consuming job",
            }
        )
        assert isinstance(input_queue, asyncio.Queue)

        while True:
            item = await input_queue.get()
            if item is None:
                break

            retry_count = 0
            original_item = item
            if isinstance(item, Dict) and "_retry_metadata" in item:
                retry_count = item["_retry_metadata"]["retry_count"]
                original_item = item["_retry_metadata"]["original_item"]

            try:
                result = await worker_func(original_item, params)
                if result is None:
                    continue

                if output_queue:
                    if isinstance(result, List):
                        for item in result:
                            await output_queue.put(item)
                    else:
                        await output_queue.put(result)

            except Exception as e:
                if retry_count < 3:
                    logger.error(
                        f"{worker_name} Worker {worker_id} "
                        f"failed to process item after {retry_count} retries: {e}"
                    )

                    backoff_time = min(30, (2**retry_count) + random.uniform(0, 1))
                    retry_item = {
                        "_retry_metadata": {
                            "retry_count": retry_count + 1,
                            "original_item": original_item,
                        }
                    }

                    await asyncio.sleep(backoff_time)
                    await input_queue.put(retry_item)
                else:
                    logger.error(
                        {
                            "log_type": "item_worker_consuming_failed",
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


async def worker_supervisor(
    worker_name: str,
    worker_func: Callable[[Any, Any], Any] | Callable[[Any], Any],
    num_workers: int,
    input_queue: Optional[asyncio.Queue] = None,
    output_queue: Optional[asyncio.Queue] = None,
    num_next_workers: Optional[int] = None,
    max_retries: int = 3,
    params: Optional[Any] = None,
):
    """
    If no input_queue, the work is producing job
    If no output_queue, the work is consuming job
    If both are provided, the work is producing and consuming job

    Worker function should be a coroutine function
    Worker function's parameters will be passed by kwargs
    """

    ## Init workers
    def create_workers(worker_count: int):
        """Create a list of worker tasks"""
        workers = []
        for i in range(worker_count):
            workers.append(
                asyncio.create_task(
                    _create_worker(
                        worker_name, i, worker_func, input_queue, output_queue, params
                    )
                )
            )
        return workers
    
    workers = create_workers(num_workers)

    for retry_attempt in range(max_retries + 1):
        logger.info(
            {
                "log_type": "item_supervisor_attempt",
                "log_data": {
                    "worker_name": worker_name,
                    "worker_count": len(workers),
                    "retry_attempt": retry_attempt,
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
                        "log_type": "item_worker_failed",
                        "log_data": {
                            "worker_name": worker_name,
                            "worker_id": i,
                            "error": str(result),
                        },
                    }
                )
                failed_worker_indices.append(i)
            else:
                logger.info(
                    {
                        "log_type": "item_worker_completed",
                        "log_data": {
                            "worker_name": worker_name,
                            "worker_id": i,
                            "retry_attempt": retry_attempt,
                        },
                    }
                )

        # If no failures, done
        if not failed_worker_indices:
            logger.info(
                {
                    "log_type": "item_supervisor_completed",
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
                    "log_type": "item_supervisor_max_retries_exceeded",
                    "log_data": {
                        "worker_name": worker_name,
                        "total_attempts": retry_attempt,
                        "successful_workers": len(workers),
                    },
                }
            )
            raise Exception(f"Item supervisor failed to complete after {max_retries} retries")

        # Re-create failed workers
        workers = create_workers(len(failed_worker_indices))
        logger.info(
            {
                "log_type": "item_supervisor_recreate_workers",
                "log_data": {
                    "worker_name": worker_name,
                    "total_attempts": retry_attempt,
                    "failed_workers": len(failed_worker_indices),
                },
            }
        )

    if output_queue:
        for _ in range(num_next_workers):
            await output_queue.put(None)
