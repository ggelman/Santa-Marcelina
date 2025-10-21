package br.com.godigital.padariaapi.dto;

public record ConfiguracaoBackupDTO(
        boolean backupDiarioAtivo,
        boolean backupSemanalAtivo,
        boolean notificarPorEmail) {
}