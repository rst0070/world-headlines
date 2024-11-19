package com.world_headlines.backend.core.country.repository;

import java.util.List;
import com.world_headlines.backend.core.country.models.HeadlineInfo;
import com.world_headlines.backend.core.country.models.NewsArticle;

/**
 * Provides country info and it's 
 */
public interface CountryRepository {
    
    public List<String> findAllCountryCodes();

    public HeadlineInfo findHeadlineInfo(String countryCode);

    public List<NewsArticle> findHeadlineNewsArticlesByCountryCode(String countryCode);

}
