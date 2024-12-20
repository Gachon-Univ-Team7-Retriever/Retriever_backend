package com.team7.retriever.controller;

import com.team7.retriever.entity.ChannelSimilarity;
import com.team7.retriever.service.ChSimilarityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("channel-similarity")
public class ChSimilarityController {

    @Autowired
    private ChSimilarityService chSimilarityService;

    @GetMapping("/all")
    public List<ChannelSimilarity> getAllChannelSimilarity() {
        return chSimilarityService.getAllChannelSimilarity();
    }

    @GetMapping("/id/{id}")
    public ChannelSimilarity getChannelSimilarityById(@PathVariable String id) {
        return chSimilarityService.getChannelSimilarityById(id);
    }

    @GetMapping("/chId/{channelId}")
    public ChannelSimilarity getChannelSimilarityByChannelId(@PathVariable String channelId) {
        return chSimilarityService.getChannelSimilarityByChannelId(channelId);
    }
}
