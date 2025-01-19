package com.world_headlines.backend.core.country.repository;

import java.util.*;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

import com.world_headlines.backend.core.country.models.HeadlineInfo;
import com.world_headlines.backend.core.country.models.NewsArticle;

@Repository
public class CountryRepositoryImpl implements CountryRepository {

    private JdbcTemplate jdbc;
    private NamedParameterJdbcTemplate namedJdbc;

    public CountryRepositoryImpl(JdbcTemplate jdbc, NamedParameterJdbcTemplate namedJdbc){
        this.jdbc = jdbc;
        this.namedJdbc = namedJdbc;
    }

    @Override
    public List<String> findAllCountryCodes() {
        
        List<String> result = new LinkedList<String>();

        List<Map<String, Object>> list = 
            jdbc.queryForList(
                """
                SELECT
                    country_code
                FROM
                    HEADLINE;
                """
            );

        list.forEach((row) -> {
            
            String val = (String)row.get("country_code");

            result.add(val);

        });
        
        return result;
    }

    @Override
    public HeadlineInfo findHeadlineInfo(String countryCode) {
        String query = 
            """
            SELECT
                country_code,
                country_name,
                last_update
            FROM
                HEADLINE
            WHERE
                country_code = :country_code
            """;        

        Map<String, Object> map = namedJdbc.queryForMap(
                query, 
                Map.of("country_code", countryCode)
            );

        HeadlineInfo result = new HeadlineInfo();
        result.setCountryCode(map.get("country_code").toString());
        result.setCountryName(map.get("country_name").toString());
        result.setLastUpdate(map.get("last_update") != null ? map.get("last_update").toString() : null);

        return result;
    }

    @Override
    public List<NewsArticle> findHeadlineNewsArticlesByCountryCode(String countryCode) {
    
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
            """;
        
        List<Map<String, Object>> rows = namedJdbc.queryForList(
                query,
                Map.of("country_code", countryCode)
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
