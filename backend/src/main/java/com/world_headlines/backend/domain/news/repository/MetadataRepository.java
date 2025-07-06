package com.world_headlines.backend.domain.news.repository;

import java.util.List;

import com.world_headlines.backend.domain.news.models.CountryInfo;

public interface MetadataRepository {

    /**
     * Gets all country codes
     * @return List of country codes on database
     */
    public List<String> findAllCountryCodes();

    /**
     * Gets country info by country code
     * @param countryCode
     * @return CountryInfo
     */
    public CountryInfo findCountryInfo(String countryCode);
}
