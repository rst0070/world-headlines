package com.world_headlines.backend.common.dto;

import lombok.Data;

@Data
public class ResponseDTO<T> {
    private T data;
}
