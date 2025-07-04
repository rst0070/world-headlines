package com.world_headlines.backend.domain.news.repository;

import java.util.*;

import com.world_headlines.backend.domain.news.models.NewsArticle;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

@Repository
public class NewsRepositoryImpl implements NewsRepository {
    private JdbcTemplate jdbc;
    private NamedParameterJdbcTemplate namedJdbc;

    public NewsRepositoryImpl(JdbcTemplate jdbc, NamedParameterJdbcTemplate namedJdbc){
        this.jdbc = jdbc;
        this.namedJdbc = namedJdbc;
    }

    @Override
    public List<NewsArticle> findNewsArticles(
        String countryCode, 
        ZonedDateTime fromDate, 
        ZonedDateTime toDate, 
        int size
    ) {
        String query =
            """
            SELECT
                country_code,
                url,
                title,
                description,
                image_url,
                publish_date,
                source
            FROM
                HEADLINE_ARTICLES
            WHERE
                country_code = :country_code
                AND publish_date >= CAST(:from_date AS TIMESTAMP) AND publish_date <= CAST(:to_date AS TIMESTAMP)
            ORDER BY publish_date DESC
            LIMIT :size
            """;
        
        List<Map<String, Object>> rows = namedJdbc.queryForList(
                query,
                Map.of(
                    "country_code", countryCode, 
                    "from_date", fromDate.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS")), 
                    "to_date", toDate.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS")), 
                    "size", size
                )
        );

        List<NewsArticle> result = new ArrayList<>();
        
        for(Map<String, Object> row : rows) {
            NewsArticle article = new NewsArticle();
            article.setCountryCode(row.get("country_code") != null ? row.get("country_code").toString() : null);
            article.setUrl(row.get("url") != null ? row.get("url").toString() : null);
            article.setTitle(row.get("title") != null ? row.get("title").toString() : null);
            article.setDescription(row.get("description") != null ? row.get("description").toString() : null);
            article.setImageUrl(row.get("image_url") != null ? row.get("image_url").toString() : null);
            article.setPublishDate(row.get("publish_date") != null ? row.get("publish_date").toString() : null);
            article.setSource(row.get("source") != null ? row.get("source").toString() : null);
            result.add(article);
        }

        return result;
    }
}
