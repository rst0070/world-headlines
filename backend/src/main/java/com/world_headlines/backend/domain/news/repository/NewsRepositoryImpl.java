package com.world_headlines.backend.domain.news.repository;

import java.sql.SQLException;
import java.util.*;

import com.world_headlines.backend.domain.news.models.NewsArticle;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

import org.postgresql.jdbc.PgArray;

@Repository
public class NewsRepositoryImpl implements NewsRepository {
    private JdbcTemplate jdbc;
    private NamedParameterJdbcTemplate namedJdbc;

    public NewsRepositoryImpl(JdbcTemplate jdbc, NamedParameterJdbcTemplate namedJdbc){
        this.jdbc = jdbc;
        this.namedJdbc = namedJdbc;
    }

    private String[] convertPgArrayToStringArray(Object pgArrayObj) {
        if (pgArrayObj == null) {
            return new String[0];
        }
        
        try {
            PgArray pgArray = (PgArray) pgArrayObj;
            Object[] objArray = (Object[]) pgArray.getArray();
            
            // Convert Object[] to String[]
            return Arrays.stream(objArray)
                    .map(obj -> obj != null ? obj.toString() : "")
                    .toArray(String[]::new);
        } catch (SQLException e) {
            // Log the error and return empty array
            System.err.println("Error converting PgArray to String[]: " + e.getMessage());
            return new String[0];
        } catch (ClassCastException e) {
            // Handle case where the object is not a PgArray
            System.err.println("Object is not a PgArray: " + e.getMessage());
            return new String[0];
        }
    }

    @Override
    public List<NewsArticle> findNewsArticles(
        String countryCode, 
        ZonedDateTime fromDate, 
        ZonedDateTime toDate, 
        int size,
        boolean shouldHaveImage
    ) {
        System.out.println("countryCode: " + countryCode);
        System.out.println("fromDate: " + fromDate);
        System.out.println("toDate: " + toDate);
        System.out.println("size: " + size);
        System.out.println("shouldHaveImage: " + shouldHaveImage);
        
        String query =
            """
            SELECT
                country_code,
                url,
                title,
                description,
                image_url,
                publish_date,
                source,
                en_title,
                en_description,
                en_topics,
                en_keywords
            FROM
                GNEWS_ARTICLES
            WHERE
                country_code = :country_code
                AND publish_date >= CAST(:from_date AS TIMESTAMP) AND publish_date <= CAST(:to_date AS TIMESTAMP)
            """ 
            + (shouldHaveImage ? "AND image_url IS NOT NULL \n" : "\n") 
            + """
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
            article.setEnTitle(row.get("en_title") != null ? row.get("en_title").toString() : null);
            article.setEnDescription(row.get("en_description") != null ? row.get("en_description").toString() : null);

            article.setEnTopics(convertPgArrayToStringArray(row.get("en_topics")));
            article.setEnKeywords(convertPgArrayToStringArray(row.get("en_keywords")));
            result.add(article);
        }

        return result;
    }
}
