package com.world_headlines.backend.core.country.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.world_headlines.backend.core.country.models.HeadlineInfo;
import com.world_headlines.backend.core.country.models.NewsArticle;
import com.world_headlines.backend.core.country.repository.CountryRepository;

@Service
public class HeadlineServiceImpl implements HeadlineService{

    private CountryRepository countryRepository;

    public HeadlineServiceImpl(CountryRepository countryRepository){
        this.countryRepository = countryRepository;
    }

    @Override
    public HeadlineInfo getHeadlineInfo(String countryCode){
        return countryRepository.findHeadlineInfo(countryCode);
    }

    @Override
    public List<NewsArticle> getNewsArticleList(String countryCode) {
        return countryRepository.findHeadlineNewsArticlesByCountryCode(countryCode);
    }
}
