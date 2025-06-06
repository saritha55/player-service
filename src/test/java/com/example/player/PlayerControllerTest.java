package com.example.player;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(PlayerController.class)
public class PlayerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    public void resetPlayers() {
        // Clear and reinitialize the player list before each test
        PlayerController.players.clear();
        PlayerController.players.addAll(List.of(
                new Player(1L, "Virat", "Kohli", 35),
                new Player(2L, "Rohit", "Sharma", 36),
                new Player(3L, "Jasprit", "Bumrah", 30)
        ));
    }

    @Test
    public void testGetPlayersAsAdmin() throws Exception {
        mockMvc.perform(get("/v1/players")
                .param("isAdmin", "true"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(3)))
                .andExpect(jsonPath("$[0].firstName", is("Virat")));
    }

    @Test
    public void testGetPlayersAsNonAdmin() throws Exception {
        mockMvc.perform(get("/v1/players")
                .param("isAdmin", "false"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(3)))
                // Only firstName and age fields are present for non-admin
                .andExpect(jsonPath("$[0].firstName", is("Virat")))
                .andExpect(jsonPath("$[0].age", is(35)))
                .andExpect(jsonPath("$[0].lastName").doesNotExist());
    }

    @Test
    public void testGetPlayerByIdAsAdminFound() throws Exception {
        mockMvc.perform(get("/v1/players/1")
                .param("isAdmin", "true"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName", is("Virat")))
                .andExpect(jsonPath("$.lastName", is("Kohli")))
                .andExpect(jsonPath("$.age", is(35)));
    }

    @Test
    public void testGetPlayerByIdAsNonAdminFound() throws Exception {
        mockMvc.perform(get("/v1/players/1")
                .param("isAdmin", "false"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName", is("Virat")))
                .andExpect(jsonPath("$.age", is(35)))
                .andExpect(jsonPath("$.lastName").doesNotExist());
    }

    @Test
    public void testGetPlayerByIdNotFound() throws Exception {
        mockMvc.perform(get("/v1/players/999")
                .param("isAdmin", "true"))
                .andExpect(status().isNotFound())
                .andExpect(content().string("Player not found"));
    }

    @Test
    public void testAddPlayerSuccess() throws Exception {
        Player newPlayer = new Player(4L, "MS", "Dhoni", 40);

        mockMvc.perform(post("/v1/players")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(newPlayer)))
                .andExpect(status().isCreated())
                .andExpect(content().string("Player added successfully"));
    }

    @Test
    public void testAddPlayerConflict() throws Exception {
        // Try to add a player with existing ID = 1L
        Player existingPlayer = new Player(1L, "Someone", "Else", 25);

        mockMvc.perform(post("/v1/players")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(existingPlayer)))
                .andExpect(status().isConflict())
                .andExpect(content().string("Player with this ID already exists"));
    }

    @Test
    public void testUpdatePlayerSuccess() throws Exception {
        Player updatedPlayer = new Player(1L, "Virat", "Kohli", 36); // changed age

        mockMvc.perform(put("/v1/players/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedPlayer)))
                .andExpect(status().isOk())
                .andExpect(content().string("Player updated successfully"));
    }

    @Test
    public void testUpdatePlayerNotFound() throws Exception {
        Player updatedPlayer = new Player(999L, "Ghost", "Player", 30);

        mockMvc.perform(put("/v1/players/999")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedPlayer)))
                .andExpect(status().isNotFound())
                .andExpect(content().string("Player not found"));
    }

    @Test
    public void testDeletePlayerSuccess() throws Exception {
        mockMvc.perform(delete("/v1/players/1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Player deleted successfully"));
    }

    @Test
    public void testDeletePlayerNotFound() throws Exception {
        mockMvc.perform(delete("/v1/players/999"))
                .andExpect(status().isNotFound())
                .andExpect(content().string("Player not found"));
    }
}
