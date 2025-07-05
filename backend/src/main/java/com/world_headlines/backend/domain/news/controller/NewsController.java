package com.world_headlines.backend.domain.news.controller;

import java.util.List;
import java.util.LinkedList;

import com.world_headlines.backend.domain.news.models.NewsArticle;
import org.springframework.web.bind.annotation.RestController;

import com.world_headlines.backend.domain.news.service.MetadataService;
import com.world_headlines.backend.domain.news.service.NewsService;
import com.world_headlines.backend.common.dto.ResponseDTO;

import java.time.ZonedDateTime;

import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import lombok.Data;

@RestController
@RequestMapping("/api/v1/news")
public class NewsController {

    private MetadataService metadataService;
    private NewsService newsService;

    public NewsController(
        MetadataService metadataService,
        NewsService newsService
    ) {
        this.metadataService = metadataService;
        this.newsService = newsService;
    }

    /**
     * The snapshot means recent news articles with pics around the world
     * @return
     */
    @GetMapping("/world_snapshot")
    public ResponseDTO<List<NewsArticle>> getWorldSnapshot() {
        ZonedDateTime now = ZonedDateTime.now();
        ZonedDateTime oneDayAgo = now.minusDays(1);

        List<String> countryCodeList = metadataService.getAllCountryCodes();

        List<NewsArticle> newsArticleList = new LinkedList<>();
        for (String countryCode : countryCodeList) {
            newsArticleList.add(
                newsService.getNewsArticleList(
                    countryCode, 
                    oneDayAgo, 
                    now, 
                    1,
                    true
                ).get(0)
            );
        }

        ResponseDTO<List<NewsArticle>> response = new ResponseDTO<>();
        response.setData(newsArticleList);

        return response;
    }


    @Data
    static class NewsArticlesResponse {
        private List<NewsArticle> data;
    }

    /**
     * @param countryCode: country code, e.g. "us"
     * @param fromDateStr: must be in ISO format
     * @param toDateStr: must be in ISO format
     * @param size: number of articles to return
     * @return
     */
    @GetMapping("/articles")
    public ResponseDTO<List<NewsArticle>> getNewsArticles(
        @RequestParam String countryCode, 
        @RequestParam String fromDate, 
        @RequestParam String toDate, 
        @RequestParam int size
    ) {
        ZonedDateTime fromDateZoned = ZonedDateTime.parse(fromDate);
        ZonedDateTime toDateZoned = ZonedDateTime.parse(toDate);

        System.out.println("fromDate: " + fromDate);
        System.out.println("toDate: " + toDate);
        System.out.println("size: " + size);

        List<NewsArticle> newsArticleList = newsService.getNewsArticleList(countryCode, fromDateZoned, toDateZoned, size, false);

        ResponseDTO<List<NewsArticle>> response = new ResponseDTO<>();
        response.setData(newsArticleList);
        return response;
    }

}
