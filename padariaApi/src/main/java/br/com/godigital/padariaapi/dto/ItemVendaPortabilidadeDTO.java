package br.com.godigital.padariaapi.dto;

import java.math.BigDecimal;

public record ItemVendaPortabilidadeDTO(
        String nomeProduto,
        int quantidade,
        BigDecimal precoUnitario) {
}