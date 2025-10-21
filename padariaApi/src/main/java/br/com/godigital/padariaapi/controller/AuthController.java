package br.com.godigital.padariaapi.controller;

import br.com.godigital.padariaapi.model.Usuario;
import br.com.godigital.padariaapi.repository.UsuarioRepository;
import br.com.godigital.padariaapi.util.JwtUtil;
import br.com.godigital.padariaapi.dto.RefreshTokenRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Collections;

@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "http://localhost:3000")
public class AuthController {

    private static final String ERROR_KEY = "error";
    private static final String ACCESS_TOKEN_KEY = "accessToken";
    private static final String REFRESH_TOKEN_KEY = "refreshToken";
    private static final String TOKEN_TYPE_KEY = "tokenType";
    private static final String BEARER = "Bearer";
    private static final String EXPIRES_IN_KEY = "expiresIn";
    private static final int TOKEN_EXPIRY_SECONDS = 86400; // 24 hours
    private static final String INVALID_REFRESH_TOKEN = "Invalid refresh token";
    
    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;
    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;
    private final UserDetailsService userDetailsService;

    public AuthController(AuthenticationManager authenticationManager, JwtUtil jwtUtil,
            UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder,
            UserDetailsService userDetailsService) {
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
        this.userDetailsService = userDetailsService;
    }

    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> login(@RequestBody AuthRequest authRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(authRequest.getEmail(), authRequest.getSenha()));

        Usuario usuario = (Usuario) authentication.getPrincipal();

        usuario.setUltimoAcesso(LocalDateTime.now());
        usuarioRepository.save(usuario);

        String accessToken = jwtUtil.generateToken(usuario);
        String refreshToken = jwtUtil.generateRefreshToken(usuario);

        Map<String, Object> userResponse = createUserResponse(usuario);
        Map<String, Object> response = createTokenResponse(accessToken, refreshToken, userResponse);

        return ResponseEntity.ok(response);
    }

    @PostMapping("/refresh")
    public ResponseEntity<Map<String, Object>> refreshToken(@RequestBody RefreshTokenRequest refreshRequest) {
        try {
            String refreshToken = refreshRequest.getRefreshToken();
            
            if (refreshToken == null || !jwtUtil.isValidRefreshToken(refreshToken)) {
                return ResponseEntity.badRequest().body(Map.of(ERROR_KEY, INVALID_REFRESH_TOKEN));
            }

            String username = jwtUtil.extractUsernameFromRefreshToken(refreshToken);
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);
            
            if (!jwtUtil.validateRefreshToken(refreshToken, userDetails)) {
                return ResponseEntity.badRequest().body(Map.of(ERROR_KEY, INVALID_REFRESH_TOKEN));
            }

            // Generate new tokens
            String newAccessToken = jwtUtil.generateToken(userDetails);
            String newRefreshToken = jwtUtil.generateRefreshToken(userDetails);

            Map<String, Object> response = createTokenResponse(newAccessToken, newRefreshToken, null);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(ERROR_KEY, INVALID_REFRESH_TOKEN));
        }
    }

    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@RequestBody Usuario usuario) {
        if (usuarioRepository.findByEmail(usuario.getEmail()).isPresent()) {
            return ResponseEntity.badRequest().body("Erro: O email já está em uso!");
        }
        usuario.setSenha(passwordEncoder.encode(usuario.getSenha()));
        usuarioRepository.save(usuario);
        return ResponseEntity.ok("Usuário registrado com sucesso!");
    }

    private Map<String, Object> createUserResponse(Usuario usuario) {
        Map<String, Object> userResponse = new HashMap<>();
        userResponse.put("id", usuario.getId());
        userResponse.put("nome", usuario.getNome());
        userResponse.put("email", usuario.getEmail());
        userResponse.put("perfil", usuario.getRole() != null ? usuario.getRole().toLowerCase() : null);
        userResponse.put("permissoes", getPermissionsFromRole(usuario.getRole()));
        return userResponse;
    }

    private Map<String, Object> createTokenResponse(String accessToken, String refreshToken, Map<String, Object> userResponse) {
        Map<String, Object> response = new HashMap<>();
        response.put(ACCESS_TOKEN_KEY, accessToken);
        response.put(REFRESH_TOKEN_KEY, refreshToken);
        response.put(TOKEN_TYPE_KEY, BEARER);
        response.put(EXPIRES_IN_KEY, TOKEN_EXPIRY_SECONDS);
        if (userResponse != null) {
            response.put("user", userResponse);
        }
        return response;
    }

    private List<String> getPermissionsFromRole(String role) {
        if ("ADMINISTRADOR".equalsIgnoreCase(role)) {
            return List.of("vendas", "produtos", "clientes", "estoque", "relatorios", "usuarios", "backup",
                    "configuracoes", "ia/previsao");
        } else if ("GERENTE".equalsIgnoreCase(role)) {
            return List.of("vendas", "produtos", "clientes", "estoque", "relatorios", "backup");
        } else if ("FUNCIONARIO".equalsIgnoreCase(role)) {
            return List.of("vendas", "clientes");
        }
        return Collections.emptyList();
    }

    public static class AuthRequest {
        private String email;
        private String senha;

        public String getEmail() {
            return email;
        }

        public void setEmail(String email) {
            this.email = email;
        }

        public String getSenha() {
            return senha;
        }

        public void setSenha(String senha) {
            this.senha = senha;
        }
    }
}