package com.world_headlines.backend.domain.news.service;

import java.time.ZonedDateTime;
import java.util.List;

import com.world_headlines.backend.domain.news.models.NewsArticle;

public interface NewsService {

    public List<NewsArticle> getNewsArticleList(
        String countryCode, 
        ZonedDateTime fromDate, 
        ZonedDateTime toDate, 
        int size
    );
}
