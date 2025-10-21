package br.com.godigital.padariaapi.repository;

import br.com.godigital.padariaapi.model.Fidelidade;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface FidelidadeRepository extends JpaRepository<Fidelidade, Long> {
    Optional<Fidelidade> findByClienteIdCliente(Long clienteId);
}