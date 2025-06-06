package com.example.player;

import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/v1/players")
public class PlayerController {

    public PlayerController() {
        System.out.println("PlayerController initialized!");
    }
    private static final List<Player> players = Arrays.asList(
        new Player(1L, "Virat", "Kohli", 35),
        new Player(2L, "Rohit", "Sharma", 36),
        new Player(3L, "Jasprit", "Bumrah", 30)
    );

    @GetMapping
    public List<?> getPlayers(@RequestParam boolean isAdmin) {
        if (isAdmin) {
            return players; // full name + age
        } else {
            return players.stream()
                .map(p -> new Object() {
                    public final String firstName = p.getFirstName();
                    public final int age = p.getAge();
                })
                .collect(Collectors.toList());
        }
    }

    @GetMapping("/{id}")
    public Object getPlayerById(@PathVariable Long id, @RequestParam boolean isAdmin) {
        return players.stream()
                .filter(p -> p.getId().equals(id))
                .findFirst()
                .map(p -> {
                    if (isAdmin) return p;
                    else return new Object() {
                        public final String firstName = p.getFirstName();
                        public final int age = p.getAge();
                    };
                })
                .orElse("Player not found");
    }
    // <-- Add this method here
    @GetMapping("/")
public String rootTest() {
    return "Player service is up";
}

}
