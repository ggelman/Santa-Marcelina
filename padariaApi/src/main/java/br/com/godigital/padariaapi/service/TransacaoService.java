package br.com.godigital.padariaapi.service;

import br.com.godigital.padariaapi.model.Transacao;
import br.com.godigital.padariaapi.repository.TransacaoRepository;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class TransacaoService {

    private final TransacaoRepository transacaoRepository;

    public TransacaoService(TransacaoRepository transacaoRepository) {
        this.transacaoRepository = transacaoRepository;
    }

    public Transacao registrarTransacao(Transacao transacao) {
        transacao.setData(LocalDateTime.now());
        return transacaoRepository.save(transacao);
    }

    public List<Transacao> listarTodas() {
        return transacaoRepository.findAll();
    }
}