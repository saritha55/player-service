package com.example.player;

import static org.junit.jupiter.api.Assertions.*;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class PlayerServiceTest {

    @Autowired
    private PlayerService playerService;

    @Test
    public void testGetAllPlayersAsAdmin() {
        List<Map<String, Object>> players = playerService.getAllPlayers(true);
        assertFalse(players.isEmpty());
        assertTrue(players.get(0).containsKey("lastName"));
    }
}
