package br.com.godigital.padariaapi.controller;

import br.com.godigital.padariaapi.model.Produto;
import br.com.godigital.padariaapi.repository.ProdutoRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/public/cardapio")
@CrossOrigin(origins = "*")
public class CardapioPublicoController {

    // Constantes para strings literals duplicadas
    private static final String SUCCESS_KEY = "success";
    private static final String PRODUTOS_KEY = "produtos";
    private static final String MESSAGE_KEY = "message";

    private final ProdutoRepository produtoRepository;

    public CardapioPublicoController(ProdutoRepository produtoRepository) {
        this.produtoRepository = produtoRepository;
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> listarProdutosCardapio() {
        try {
            List<Produto> produtos = produtoRepository.findAll();
            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                PRODUTOS_KEY, produtos
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao listar produtos: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/produtos")
    public ResponseEntity<Map<String, Object>> listarProdutos(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String categoria,
            @RequestParam(required = false) String busca) {
        try {
            PageRequest pageRequest = PageRequest.of(page, size, Sort.by("categoria").and(Sort.by("nome")));
            Page<Produto> produtosPage;

            if (categoria != null && !categoria.isEmpty()) {
                if (busca != null && !busca.isEmpty()) {
                    produtosPage = produtoRepository.findByCategoriaAndNomeContainingIgnoreCase(categoria, busca, pageRequest);
                } else {
                    produtosPage = produtoRepository.findByCategoria(categoria, pageRequest);
                }
            } else if (busca != null && !busca.isEmpty()) {
                produtosPage = produtoRepository.findByNomeContainingIgnoreCase(busca, pageRequest);
            } else {
                produtosPage = produtoRepository.findAll(pageRequest);
            }

            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                PRODUTOS_KEY, produtosPage.getContent(),
                "totalPages", produtosPage.getTotalPages(),
                "totalElements", produtosPage.getTotalElements(),
                "currentPage", page,
                "hasNext", produtosPage.hasNext(),
                "hasPrevious", produtosPage.hasPrevious()
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao listar produtos: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/categorias")
    public ResponseEntity<Map<String, Object>> listarCategorias() {
        try {
            List<String> categorias = produtoRepository.findDistinctCategorias();
            
            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                "categorias", categorias
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao listar categorias: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/categoria/{categoria}")
    public ResponseEntity<Map<String, Object>> listarProdutosPorCategoria(@PathVariable String categoria) {
        try {
            List<Produto> produtos = produtoRepository.findByCategoriaOrderByNome(categoria);
            
            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                PRODUTOS_KEY, produtos,
                "categoria", categoria,
                "total", produtos.size()
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao listar produtos da categoria: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/destaque")
    public ResponseEntity<Map<String, Object>> listarProdutosDestaque(@RequestParam(defaultValue = "6") int limite) {
        try {
            PageRequest pageRequest = PageRequest.of(0, limite, Sort.by("nome"));
            Page<Produto> produtosPage = produtoRepository.findAll(pageRequest);
            
            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                PRODUTOS_KEY, produtosPage.getContent(),
                "total", produtosPage.getContent().size()
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao listar produtos em destaque: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Map<String, Object>> obterProduto(@PathVariable Long id) {
        try {
            Produto produto = produtoRepository.findById(id)
                    .orElseThrow(() -> new RuntimeException("Produto não encontrado"));

            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                "produto", produto
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao obter produto: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/buscar")
    public ResponseEntity<Map<String, Object>> buscarProdutos(
            @RequestParam String termo,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        try {
            PageRequest pageRequest = PageRequest.of(page, size, Sort.by("nome"));
            Page<Produto> produtosPage = produtoRepository.findByNomeContainingIgnoreCaseOrDescricaoContainingIgnoreCase(
                    termo, termo, pageRequest);
            
            return ResponseEntity.ok(Map.of(
                SUCCESS_KEY, true,
                PRODUTOS_KEY, produtosPage.getContent(),
                "totalPages", produtosPage.getTotalPages(),
                "totalElements", produtosPage.getTotalElements(),
                "currentPage", page,
                "termoBusca", termo
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                SUCCESS_KEY, false,
                MESSAGE_KEY, "Erro ao buscar produtos: " + e.getMessage()
            ));
        }
    }
}
