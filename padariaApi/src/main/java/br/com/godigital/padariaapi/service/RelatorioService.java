package br.com.godigital.padariaapi.service;

import br.com.godigital.padariaapi.dto.GraficoPontoDTO;
import br.com.godigital.padariaapi.dto.ProdutoVendidoDTO;
import br.com.godigital.padariaapi.dto.ResumoFinanceiroDTO;
import br.com.godigital.padariaapi.dto.ResumoVendasDTO;
import br.com.godigital.padariaapi.model.Cliente;
import br.com.godigital.padariaapi.model.Produto;
import br.com.godigital.padariaapi.model.Transacao;
import br.com.godigital.padariaapi.model.Venda;
import br.com.godigital.padariaapi.repository.ClienteRepository;
import br.com.godigital.padariaapi.repository.ProdutoRepository;
import br.com.godigital.padariaapi.repository.TransacaoRepository;
import br.com.godigital.padariaapi.repository.VendaRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;
import java.util.Map;
import java.time.format.DateTimeFormatter;
import java.util.stream.Collectors;

@Service
public class RelatorioService {

    private final VendaRepository vendaRepository;
    private final ProdutoRepository produtoRepository;
    private final TransacaoRepository transacaoRepository;
    private final ClienteRepository clienteRepository;

    public RelatorioService(VendaRepository vendaRepository, ProdutoRepository produtoRepository,
            TransacaoRepository transacaoRepository, ClienteRepository clienteRepository) {
        this.vendaRepository = vendaRepository;
        this.produtoRepository = produtoRepository;
        this.transacaoRepository = transacaoRepository;
        this.clienteRepository = clienteRepository;
    }

    public List<Venda> gerarRelatorioVendas(LocalDate inicio, LocalDate fim) {
        LocalDateTime inicioComHora = inicio.atStartOfDay();
        LocalDateTime fimComHora = fim.atTime(LocalTime.MAX);
        return vendaRepository.findByDataBetween(inicioComHora, fimComHora);
    }

    public List<Transacao> buscarTransacoesPorPeriodo(LocalDate inicio, LocalDate fim) {
        LocalDateTime inicioComHora = inicio.atStartOfDay();
        LocalDateTime fimComHora = fim.atTime(LocalTime.MAX);
        return transacaoRepository.findByDataBetween(inicioComHora, fimComHora);
    }

    public List<Produto> gerarRelatorioEstoque() {
        return produtoRepository.findAll();
    }

    public List<Produto> gerarRelatorioEstoqueBaixo() {
        return produtoRepository.findProdutosComEstoqueBaixo();
    }

    public List<Produto> gerarRelatorioEstoqueZerado() {
        return produtoRepository.findProdutosComEstoqueZerado();
    }

    public ResumoVendasDTO getResumoDiario(LocalDate inicio, LocalDate fim) {
        LocalDateTime inicioComHora = inicio.atStartOfDay();
        LocalDateTime fimComHora = fim.atTime(LocalTime.MAX);

        // CORRIGIDO: Usar BigDecimal desde o início
        BigDecimal faturamento = vendaRepository.sumValorTotalByDataBetween(inicioComHora, fimComHora)
                .orElse(BigDecimal.ZERO);
        Long quantidadeVendas = vendaRepository.countVendasByDataBetween(inicioComHora, fimComHora).orElse(0L);

        List<ProdutoVendidoDTO> maisVendidos = vendaRepository.findTopSoldProductsAsDTO(inicioComHora, fimComHora);

        ResumoVendasDTO resumo = new ResumoVendasDTO();
        resumo.setTotalFaturamento(faturamento);
        resumo.setQuantidadeVendas(quantidadeVendas);
        resumo.setProdutosMaisVendidos(maisVendidos);

        if (quantidadeVendas > 0) {
            resumo.setTicketMedio(faturamento.divide(new BigDecimal(quantidadeVendas), 2, RoundingMode.HALF_UP));
        } else {
            resumo.setTicketMedio(BigDecimal.ZERO);
        }

        return resumo;
    }

    public ResumoFinanceiroDTO getFinanceiro(LocalDate inicio, LocalDate fim) {
        LocalDateTime inicioComHora = inicio.atStartOfDay();
        LocalDateTime fimComHora = fim.atTime(LocalTime.MAX);

        List<Transacao> transacoes = transacaoRepository.findByDataBetween(inicioComHora, fimComHora);

        BigDecimal receitaTransacoesManuais = transacoes.stream()
                .filter(t -> t.getTipo() == Transacao.TipoTransacao.RECEITA && t.getValor() != null && !t.getDescricao().startsWith("Venda #"))
                .map(Transacao::getValor)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal despesaTransacoes = transacoes.stream()
                .filter(t -> t.getTipo() == Transacao.TipoTransacao.DESPESA && t.getValor() != null)
                .map(Transacao::getValor)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal totalVendas = vendaRepository.sumValorTotalByDataBetween(inicioComHora, fimComHora)
                .orElse(BigDecimal.ZERO);

        BigDecimal receitaFinal = totalVendas.add(receitaTransacoesManuais);
        BigDecimal despesaFinal = despesaTransacoes;
        BigDecimal lucroFinal = receitaFinal.subtract(despesaFinal);

        ResumoFinanceiroDTO financeiro = new ResumoFinanceiroDTO();
        financeiro.setReceita(receitaFinal);
        financeiro.setDespesa(despesaFinal);
        financeiro.setLucro(lucroFinal);
        financeiro.setTotalVendas(totalVendas);
        return financeiro;
    }

    public List<Map<String, Object>> getVendasPorProduto() {
        return vendaRepository.findVendasPorProduto();
    }

    public List<Cliente> getAniversariantesDoDia() {
        return clienteRepository.findAniversariantesDoDia();
    }

    public List<GraficoPontoDTO> getEvolucaoFinanceira(LocalDate inicio, LocalDate fim) {
        LocalDateTime inicioComHora = inicio.atStartOfDay();
        LocalDateTime fimComHora = fim.atTime(LocalTime.MAX);

        List<Object[]> resultados = vendaRepository.findFaturamentoDiarioRaw(inicioComHora, fimComHora);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM");

        return resultados.stream()
                .map(resultado -> {
                    LocalDate data = ((java.sql.Date) resultado[0]).toLocalDate();
                    BigDecimal valor = (BigDecimal) resultado[1];
                    return new GraficoPontoDTO(data.format(formatter), valor);
                })
                .collect(Collectors.toList());
    }
}