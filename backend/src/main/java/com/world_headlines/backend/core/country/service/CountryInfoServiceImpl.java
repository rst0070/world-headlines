package com.world_headlines.backend.core.country.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.world_headlines.backend.core.country.repository.CountryRepository;

@Service
public class CountryInfoServiceImpl implements CountryInfoService {

    private CountryRepository countryRepository;

    public CountryInfoServiceImpl(CountryRepository countryRepository){
        this.countryRepository = countryRepository;
    }

    @Override
    public List<String> getAllCountryCodes() {
        return countryRepository.findAllCountryCodes();
    }
    
}
