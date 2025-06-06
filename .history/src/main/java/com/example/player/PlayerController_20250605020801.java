package com.example.player;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/v1/players")
public class PlayerController {

    static final List<Player> players = new CopyOnWriteArrayList<>(
        List.of(
            new Player(1L, "Virat", "Kohli", 35),
            new Player(2L, "Rohit", "Sharma", 36),
            new Player(3L, "Jasprit", "Bumrah", 30)
        )
    );

    // GET all players
    @GetMapping
    public List<?> getPlayers(@RequestParam boolean isAdmin) {
        if (isAdmin) {
            return players;
        } else {
            return players.stream()
                .map(p -> new Object() {
                    public final String firstName = p.getFirstName();
                    public final int age = p.getAge();
                })
                .collect(Collectors.toList());
        }
    }

    // GET player by ID
    @GetMapping("/{id}")
    public ResponseEntity<?> getPlayerById(@PathVariable Long id, @RequestParam boolean isAdmin) {
        return players.stream()
                .filter(p -> p.getId().equals(id))
                .findFirst()
                .map(p -> {
                    if (isAdmin) return ResponseEntity.ok(p);
                    else return ResponseEntity.ok(new Object() {
                        public final String firstName = p.getFirstName();
                        public final int age = p.getAge();
                    });
                })
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND).body("Player not found"));
    }

    // POST add new player
    @PostMapping
    public ResponseEntity<String> addPlayer(@RequestBody Player newPlayer) {
        boolean exists = players.stream().anyMatch(p -> p.getId().equals(newPlayer.getId()));
        if (exists) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body("Player with this ID already exists");
        }
        players.add(newPlayer);
        return ResponseEntity.status(HttpStatus.CREATED).body("Player added successfully");
    }

    // PUT update existing player
    @PutMapping("/{id}")
    public ResponseEntity<String> updatePlayer(@PathVariable Long id, @RequestBody Player updatedPlayer) {
        for (int i = 0; i < players.size(); i++) {
            if (players.get(i).getId().equals(id)) {
                players.set(i, updatedPlayer);
                return ResponseEntity.ok("Player updated successfully");
            }
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Player not found");
    }

    // DELETE player
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deletePlayer(@PathVariable Long id) {
        boolean removed = players.removeIf(p -> p.getId().equals(id));
        if (removed) {
            return ResponseEntity.ok("Player deleted successfully");
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Player not found");
        }
    }
}
