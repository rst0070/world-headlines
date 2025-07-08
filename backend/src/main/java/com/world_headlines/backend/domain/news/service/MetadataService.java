package com.world_headlines.backend.domain.news.service;

import java.util.List;

import com.world_headlines.backend.domain.news.models.CountryInfo;

public interface MetadataService {

    public CountryInfo getCountryInfo(String countryCode);

    public List<String> getAllCountryCodes();

}
