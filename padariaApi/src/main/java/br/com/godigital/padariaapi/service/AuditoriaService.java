package br.com.godigital.padariaapi.service;

import br.com.godigital.padariaapi.model.LogAuditoria;
import br.com.godigital.padariaapi.repository.LogAuditoriaRepository;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
public class AuditoriaService {

    private final LogAuditoriaRepository logAuditoriaRepository;

    public AuditoriaService(LogAuditoriaRepository logAuditoriaRepository) {
        this.logAuditoriaRepository = logAuditoriaRepository;
    }

    public void registrarLog(String acao, String detalhes) {
        String usuarioEmail = SecurityContextHolder.getContext().getAuthentication().getName();
        LogAuditoria log = new LogAuditoria(usuarioEmail, acao, detalhes);
        logAuditoriaRepository.save(log);
    }
}