import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function HomePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simular carregamento
    setTimeout(() => {
      setLoading(false);
    }, 2000);
  }, []);

  const handleGoToLogin = () => {
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-orange-600 mx-auto"></div>
          <p className="mt-4 text-[var(--synvia-text-secondary)]">Carregando Sistema HTTPS...</p>
          <p className="text-sm text-gray-400">Inicializando componentes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FBF5F3] to-[#E8EDF5]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-[var(--synvia-space-cadet)] mb-4">
            {BRAND.name} Experience
          </h1>
          <p className="text-xl text-[var(--synvia-text-secondary)] mb-8">
            {BRAND.tagline}
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white/90 p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">✅</div>
              <h3 className="text-lg font-semibold text-green-700 mb-2">Frontend</h3>
              <p className="text-sm text-[var(--synvia-text-secondary)]">Next.js rodando em HTTP</p>
              <p className="text-xs text-gray-500">Porta 3000</p>
            </div>
            
            <div className="bg-white/90 p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🔒</div>
              <h3 className="text-lg font-semibold text-blue-700 mb-2">Backend</h3>
              <p className="text-sm text-[var(--synvia-text-secondary)]">Spring Boot em HTTP</p>
              <p className="text-xs text-gray-500">Porta 8080</p>
            </div>
            
            <div className="bg-white/90 p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🤖</div>
              <h3 className="text-lg font-semibold text-purple-700 mb-2">AI Service</h3>
              <p className="text-sm text-[var(--synvia-text-secondary)]">Python Flask em HTTP</p>
              <p className="text-xs text-gray-500">Porta 5001</p>
            </div>
          </div>
          
          <div className="bg-white/90 p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-[var(--synvia-space-cadet)] mb-6">
              🎉 Ambiente HTTP pronto para desenvolvimento
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
              <div>
                <h3 className="font-semibold text-green-700 mb-3">✅ Componentes Funcionando:</h3>
                <ul className="text-sm text-[var(--synvia-text-secondary)] space-y-2">
                  <li>• Frontend Synvia em HTTP</li>
                  <li>• Backend Spring Boot em HTTP</li>
                  <li>• AI Service Python Flask em HTTP</li>
                  <li>• Comunicação local sem TLS</li>
                  <li>• Scripts de automação criados</li>
                </ul>
              </div>
              
              <div>
                <h3 className="font-semibold text-blue-700 mb-3">🔗 URLs de Acesso (modo HTTP):</h3>
                <ul className="text-sm text-[var(--synvia-text-secondary)] space-y-2">
                  <li>• Frontend: <code className="bg-gray-100 px-1 rounded">http://localhost:3000</code></li>
                  <li>• Backend: <code className="bg-gray-100 px-1 rounded">http://localhost:8080/api</code></li>
                  <li>• AI Service: <code className="bg-gray-100 px-1 rounded">http://localhost:5001/api/ai</code></li>
                  <li>• Swagger: <code className="bg-gray-100 px-1 rounded">http://localhost:8080/swagger-ui.html</code></li>
                </ul>
              </div>
            </div>
            
            <div className="mt-8">
              <button
                onClick={handleGoToLogin}
                className="bg-[var(--synvia-accent-primary)] hover:bg-[#255f91] text-white font-medium py-3 px-6 rounded-lg transition-colors"
              >
                Acessar Sistema → Login
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}