package com.world_headlines.backend.user.controller;

import java.util.Map;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.world_headlines.backend.common.dto.ResponseDTO;

@RestController
@RequestMapping("/api/v1/sign")
public class SignController {

    @PostMapping("/check-account")
    public ResponseDTO<Boolean> checkAccount(@RequestBody Map<String, String> request) {
        ResponseDTO<Boolean> responseDTO = new ResponseDTO<>();
        responseDTO.setData(true);
        return responseDTO;
    }

}
