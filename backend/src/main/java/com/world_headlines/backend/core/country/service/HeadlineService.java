package com.world_headlines.backend.core.country.service;

import java.util.List;
import com.world_headlines.backend.core.country.models.*;

/**
 * Provides headline information by country
 */
public interface HeadlineService {

    public HeadlineInfo getHeadlineInfo(String countryCode);

    public List<NewsArticle> getNewsArticleList(String countryCode);
    
}
