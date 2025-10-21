package br.com.godigital.padariaapi.dto;

import java.time.LocalDate;

public record ClienteUpdateRequest(
        String nome,
        String telefone,
        String email,
        LocalDate dataNascimento,
        String observacoes,
        Boolean participaFidelidade) {
}