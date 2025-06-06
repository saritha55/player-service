package com.example.player;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(PlayerController.class)
public class PlayerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper; // to serialize/deserialize JSON

    private Player samplePlayer;

    @BeforeEach
    public void setup() {
        samplePlayer = new Player(10L, "Sachin", "Tendulkar", 48);
    }

    @Test
    public void testGetAllPlayersAsAdmin() throws Exception {
        mockMvc.perform(get("/v1/players")
                .param("isAdmin", "true"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(3)))) // original 3 players exist
                .andExpect(jsonPath("$[0].lastName").exists());
    }

    @Test
    public void testGetAllPlayersAsNonAdmin() throws Exception {
        mockMvc.perform(get("/v1/players")
                .param("isAdmin", "false"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(3))))
                .andExpect(jsonPath("$[0].firstName").exists())
                .andExpect(jsonPath("$[0].lastName").doesNotExist());
    }

    @Test
    public void testGetPlayerByIdFoundAdmin() throws Exception {
        mockMvc.perform(get("/v1/players/1")
                .param("isAdmin", "true"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName", is("Virat")))
                .andExpect(jsonPath("$.lastName", is("Kohli")));
    }

    @Test
    public void testGetPlayerByIdFoundNonAdmin() throws Exception {
        mockMvc.perform(get("/v1/players/1")
                .param("isAdmin", "false"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName", is("Virat")))
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
        mockMvc.perform(post("/v1/players")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(samplePlayer)))
                .andExpect(status().isCreated())
                .andExpect(content().string("Player added successfully"));
    }

    @Test
    public void testAddPlayerConflict() throws Exception {
        // Adding existing player id 1 again should return conflict
        Player existingPlayer = new Player(1L, "Duplicate", "Player", 30);

        mockMvc.perform(post("/v1/players")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(existingPlayer)))
                .andExpect(status().isConflict())
                .andExpect(content().string("Player with this ID already exists"));
    }

    @Test
    public void testUpdatePlayerSuccess() throws Exception {
        Player updatedPlayer = new Player(1L, "Virat", "Kohli", 36);

        mockMvc.perform(put("/v1/players/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedPlayer)))
                .andExpect(status().isOk())
                .andExpect(content().string("Player updated successfully"));
    }

    @Test
    public void testUpdatePlayerNotFound() throws Exception {
        Player updatedPlayer = new Player(999L, "Unknown", "Player", 40);

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
