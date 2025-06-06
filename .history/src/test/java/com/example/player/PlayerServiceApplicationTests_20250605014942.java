package com.example.player;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class PlayerServiceApplicationTests {

    @Autowired
    private PlayerService service;

    @Test
    void contextLoads() {
        // This test ensures the Spring context loads successfully
    }

    @Test
    void testGetAllPlayersAsAdmin() {
        List<Map<String, Object>> players = service.getAllPlayers(true);
        assertFalse(players.isEmpty(), "Players list should not be empty for admin");
        assertTrue(players.get(0).containsKey("lastName"), "Player object should contain lastName key");
    }
}
