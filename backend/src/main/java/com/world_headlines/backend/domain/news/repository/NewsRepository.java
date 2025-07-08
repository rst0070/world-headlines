package com.world_headlines.backend.domain.news.repository;

import java.util.List;
import java.time.ZonedDateTime;

import com.world_headlines.backend.domain.news.models.NewsArticle;

public interface NewsRepository {
    /**
     * Gets news articles by country code, from date, to date, and size
     * @param countryCode
     * @param fromDate
     * @param toDate
     * @param size
     * @return List of NewsArticles
     */
    public List<NewsArticle> findNewsArticles(
        String countryCode, 
        ZonedDateTime fromDate, 
        ZonedDateTime toDate, 
        int size,
        boolean shouldHaveImage
    );
}
