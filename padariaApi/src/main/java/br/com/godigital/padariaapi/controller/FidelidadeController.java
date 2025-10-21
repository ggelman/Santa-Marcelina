package br.com.godigital.padariaapi.controller;

import br.com.godigital.padariaapi.model.Fidelidade;
import br.com.godigital.padariaapi.service.FidelidadeService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/fidelidade")
@CrossOrigin(origins = "http://localhost:3000")
public class FidelidadeController {

    private final FidelidadeService fidelidadeService;

    public FidelidadeController(FidelidadeService fidelidadeService) {
        this.fidelidadeService = fidelidadeService;
    }

    @PostMapping("/clientes/{clienteId}/pontos")
    public ResponseEntity<Fidelidade> ajustarPontos(@PathVariable Long clienteId,
            @RequestBody Map<String, Integer> request) {
        Integer pontos = request.get("pontos");
        if (pontos == null) {
            return ResponseEntity.badRequest().build();
        }
        Fidelidade fidelidadeAtualizada = fidelidadeService.ajustarPontos(clienteId, pontos);
        return ResponseEntity.ok(fidelidadeAtualizada);
    }
}