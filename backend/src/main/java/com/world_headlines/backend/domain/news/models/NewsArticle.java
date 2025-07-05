package com.world_headlines.backend.domain.news.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class NewsArticle {

    @JsonProperty("country_code")
    private String countryCode;

    @JsonProperty("url")
    private String url;
    
    @JsonProperty("title")
    private String title;

    @JsonProperty("description")
    private String description;

    @JsonProperty("image_url")
    private String imageUrl;

    @JsonProperty("publish_date")
    private String publishDate;

    @JsonProperty("source")
    private String source;

    @JsonProperty("en_title")
    private String enTitle;

    @JsonProperty("en_description")
    private String enDescription;

    @JsonProperty("en_topics")
    private String[] enTopics;

    @JsonProperty("en_keywords")
    private String[] enKeywords;
}
