package com.world_headlines.backend.domain.news.service;

import java.util.List;
import java.time.ZonedDateTime;
import org.springframework.stereotype.Service;

import com.world_headlines.backend.domain.news.models.NewsArticle;
import com.world_headlines.backend.domain.news.repository.NewsRepository;

@Service
public class NewsServiceImpl implements NewsService {

    private NewsRepository newsRepository;

    public NewsServiceImpl(NewsRepository newsRepository) {
        this.newsRepository = newsRepository;
    }

    @Override
    public List<NewsArticle> getNewsArticleList(
        String countryCode, 
        ZonedDateTime fromDate, 
        ZonedDateTime toDate, 
        int size,
        boolean shouldHaveImage
    ) {
        return newsRepository.findNewsArticles(countryCode, fromDate, toDate, size, shouldHaveImage);
    }
}
