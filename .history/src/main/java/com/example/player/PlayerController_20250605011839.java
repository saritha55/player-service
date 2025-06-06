package com.example.player;

import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/v1/players")
public class PlayerController {

    private static final List<Player> players = Arrays.asList(
        new Player(1L, "Virat", "Kohli", 35),
        new Player(2L, "Rohit", "Sharma", 36),
        new Player(3L, "Jasprit", "Bumrah", 30)
    );

    // Simple test endpoint to check if controller is working
    @GetMapping("/test")
    public String test() {
        return "Player controller is working";
    }

    // Get all players
    @GetMapping
    public List<?> getPlayers(@RequestParam boolean isAdmin) {
        if (isAdmin) {
            return players; // full player objects with all details
        } else {
            // Return limited data (firstName + age)
            return players.stream()
                    .map(p -> new Object() {
                        public final String firstName = p.getFirstName();
                        public final int age = p.getAge();
                    })
                    .collect(Collectors.toList());
        }
    }

    // Get player by id
    @GetMapping("/{id}")
    public Object getPlayerById(@PathVariable Long id, @RequestParam boolean isAdmin) {
        return players.stream()
                .filter(p -> p.getId().equals(id))
                .findFirst()
                .map(p -> {
                    if (isAdmin) {
                        return p;
                    } else {
                        return new Object() {
                            public final String firstName = p.getFirstName();
                            public final int age = p.getAge();
                        };
                    }
                })
                .orElse("Player not found");
    }
}
