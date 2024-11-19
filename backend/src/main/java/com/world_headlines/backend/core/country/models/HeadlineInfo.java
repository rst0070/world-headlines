package com.world_headlines.backend.core.country.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Stores basic information of headline of a country
 */
@Data
public class HeadlineInfo {

    @JsonProperty("country_code")
    private String countryCode;

    @JsonProperty("country_name")
    private String countryName;

    @JsonProperty("last_update")
    private String lastUpdate;
}
