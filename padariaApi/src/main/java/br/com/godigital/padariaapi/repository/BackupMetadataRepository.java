package br.com.godigital.padariaapi.repository;

import br.com.godigital.padariaapi.model.BackupMetadata;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BackupMetadataRepository extends JpaRepository<BackupMetadata, Long> {
}