package com.world_headlines.backend.domain.news.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.world_headlines.backend.domain.news.service.MetadataService;
import com.world_headlines.backend.common.dto.ResponseDTO;
import java.util.*;

import lombok.Data;

import com.world_headlines.backend.domain.news.models.CountryInfo;

/**
 * Controller for news about specific country
 */
@RestController
@RequestMapping("/api/v1/country")
public class MetadataController {

    private MetadataService metadataService;

    public MetadataController(MetadataService metadataService){
        this.metadataService = metadataService;
    }


    @Data
    static class CountryCodesResponse {
        private List<String> data;
    }

    @GetMapping("/country_codes")
    public ResponseDTO<List<String>> getAllCountryCodes(){
        List<String> countryCodeList = metadataService.getAllCountryCodes();

        ResponseDTO<List<String>> response = new ResponseDTO<>();
        response.setData(countryCodeList);
        
        return response;
    }

    /**
     * Gets basic info of headline from the country
     * 
     * @param country_code: country code to get headline info 
     * @return CountryHeadlineInfo
     */
    @GetMapping("/country_info")
    public ResponseDTO<CountryInfo> getCountryInfo(@RequestParam() String country_code) {

        CountryInfo info = metadataService.getCountryInfo(country_code);
        ResponseDTO<CountryInfo> response = new ResponseDTO<>();
        response.setData(info);

        return response;
    }
}
