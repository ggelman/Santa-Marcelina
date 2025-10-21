package br.com.godigital.padariaapi.service;

import br.com.godigital.padariaapi.exception.RecursoNaoEncontradoException;
import br.com.godigital.padariaapi.exception.ValidacaoNegocioException;
import br.com.godigital.padariaapi.model.Fidelidade;
import br.com.godigital.padariaapi.repository.FidelidadeRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class FidelidadeService {

    private final FidelidadeRepository fidelidadeRepository;

    public FidelidadeService(FidelidadeRepository fidelidadeRepository) {
        this.fidelidadeRepository = fidelidadeRepository;
    }

    @Transactional
    public Fidelidade ajustarPontos(Long clienteId, int pontosParaAjustar) {
        Fidelidade fidelidade = fidelidadeRepository.findByClienteIdCliente(clienteId)
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Programa de fidelidade não encontrado para o cliente: " + clienteId));

        int novosPontos = fidelidade.getPontos() + pontosParaAjustar;

        if (novosPontos < 0) {
            throw new ValidacaoNegocioException("Pontos insuficientes para resgate.");
        }

        fidelidade.setPontos(novosPontos);

        return fidelidadeRepository.save(fidelidade);
    }
}