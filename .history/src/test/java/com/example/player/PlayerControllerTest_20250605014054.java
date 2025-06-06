package com.example.player;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class PlayerControllerTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void contextLoads() {
        // Make a GET request to the players endpoint with isAdmin=true
        ResponseEntity<String> response = restTemplate.getForEntity("/v1/players?isAdmin=true", String.class);

        // Assert that the HTTP status is 200 OK
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);

        // Optional: You can add further assertions to check the response body if you want
        // For example, check if response body contains a known player name
        assertThat(response.getBody()).contains("Virat");
    }
}
