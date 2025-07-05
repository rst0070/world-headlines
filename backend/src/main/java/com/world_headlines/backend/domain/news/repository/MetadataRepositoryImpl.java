package com.world_headlines.backend.domain.news.repository;

import java.util.*;

import org.springframework.stereotype.Repository;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;

import com.world_headlines.backend.domain.news.models.CountryInfo;

@Repository
public class MetadataRepositoryImpl implements MetadataRepository {

    private JdbcTemplate jdbc;
    private NamedParameterJdbcTemplate namedJdbc;

    public MetadataRepositoryImpl(JdbcTemplate jdbc, NamedParameterJdbcTemplate namedJdbc){
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
                    GNEWS_HEADLINE;
                """
            );

        list.forEach((row) -> {
            
            String val = (String)row.get("country_code");

            result.add(val);

        });
        
        return result;
    }

    @Override
    public CountryInfo findCountryInfo(String countryCode) {
        String query = 
            """
            SELECT
                country_code,
                country_name,
                last_update
            FROM
                GNEWS_HEADLINE
            WHERE
                country_code = :country_code
            """;        

        Map<String, Object> map = namedJdbc.queryForMap(
                query, 
                Map.of("country_code", countryCode)
            );

        CountryInfo result = new CountryInfo();
        result.setCountryCode(map.get("country_code").toString());
        result.setCountryName(map.get("country_name").toString());
        result.setLastUpdate(map.get("last_update") != null ? map.get("last_update").toString() : null);

        return result;
    }
}
