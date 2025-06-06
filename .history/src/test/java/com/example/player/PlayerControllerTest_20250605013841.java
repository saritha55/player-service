package com.example.player;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.ResponseEntity;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class PlayerControllerTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void contextLoads() {
        // Basic test to check if controller is up and responding
        ResponseEntity<String> response = restTemplate.getForEntity("/v1/players?isAdmin=true", String.class);
        assertThat(response.getStatusCodeValue()).isEqualTo(200);
    }
}
