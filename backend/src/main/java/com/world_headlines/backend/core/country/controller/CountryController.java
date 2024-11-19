package com.world_headlines.backend.core.country.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;

import com.world_headlines.backend.core.country.models.HeadlineInfo;
import com.world_headlines.backend.core.country.models.NewsArticle;
import com.world_headlines.backend.core.country.service.HeadlineService;
import com.world_headlines.backend.core.country.service.CountryInfoService;

@RestController
@RequestMapping("/api/country")
public class CountryController {

    private CountryInfoService countryInfoService;
    private HeadlineService countryHeadlineService;

    public CountryController(CountryInfoService countryInfoService, HeadlineService countryHeadlineService){
        this.countryInfoService = countryInfoService;
        this.countryHeadlineService = countryHeadlineService;
    }

    @GetMapping("/country_codes")
    public List<String> getAllCountryCodes(){
        List<String> countryCodeList = countryInfoService.getAllCountryCodes();
        return countryCodeList;
    }

    /**
     * Gets basic info of headline from the country
     * 
     * @param country_code: country code to get headline info 
     * @return CountryHeadlineInfo
     */
    @GetMapping("/headline_info")
    public HeadlineInfo getHeadlineInfo(@RequestParam() String country_code) {

        HeadlineInfo info = countryHeadlineService.getHeadlineInfo(country_code);

        return info;
    }

    @GetMapping("/news_articles")
    public List<NewsArticle> getNewsArticles(@RequestParam String country_code) {
        return countryHeadlineService.getNewsArticleList(country_code);
    }
    
    
}
