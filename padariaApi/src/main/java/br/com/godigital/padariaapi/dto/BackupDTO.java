package br.com.godigital.padariaapi.dto;

import br.com.godigital.padariaapi.model.Cliente;
import br.com.godigital.padariaapi.model.Produto;
import br.com.godigital.padariaapi.model.Venda;

import java.util.List;

public record BackupDTO(
                List<Cliente> clientes,
                List<Produto> produtos,
                List<Venda> vendas,
                List<UsuarioBackupDTO> usuarios) {
}