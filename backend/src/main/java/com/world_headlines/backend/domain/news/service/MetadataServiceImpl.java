package com.world_headlines.backend.domain.news.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.world_headlines.backend.domain.news.models.CountryInfo;
import com.world_headlines.backend.domain.news.models.NewsArticle;
import com.world_headlines.backend.domain.news.repository.MetadataRepository;

@Service
public class MetadataServiceImpl implements MetadataService {

    private MetadataRepository metadataRepository;

    public MetadataServiceImpl(MetadataRepository metadataRepository){
        this.metadataRepository = metadataRepository;
    }

    @Override
    public List<String> getAllCountryCodes() {
        return metadataRepository.findAllCountryCodes();
    }

    @Override
    public CountryInfo getCountryInfo(String countryCode) {
        return metadataRepository.findCountryInfo(countryCode);
    }
}
