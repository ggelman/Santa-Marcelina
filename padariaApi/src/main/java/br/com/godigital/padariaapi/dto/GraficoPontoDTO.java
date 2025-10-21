package br.com.godigital.padariaapi.dto;

import java.math.BigDecimal;

public record GraficoPontoDTO(
    String label, 
    BigDecimal valor 
) {}