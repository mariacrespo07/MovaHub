import Image from "next/image";

export default function Home() {
  return (
   <main className="min-h-screen bg-mova-bg flex flex-col">
      {/* Cabeçalho com as duas marcas */}
     <header className="grid grid-cols-3 items-center px-10 py-8">
  <div>
    <Image src="/aacd-logo.webp" alt="AACD" width={70} height={70} />
  </div>
  <div className="flex items-center justify-center gap-2">
    <Image src="/logo-icon.svg" alt="" width={40} height={40} />
    <span className="text-white text-2xl font-bold">MovaHub</span>
  </div>
  <div />
</header>

{/* Texto de propósito + frase de destaque */}
<section className="flex-1 flex flex-col items-center justify-center text-center px-6 max-w-2xl mx-auto">
  <p className="text-white text-xl md:text-2xl font-semibold leading-relaxed">
    A AACD é uma organização sem fins lucrativos referência em ortopedia
    e reabilitação. Desde 1950, já são mais de 70 milhões de atendimentos,
    sempre com foco em autonomia, inclusão social e qualidade de vida para quem passa por
    seus cuidados.
  </p>

  <p className="mt-6 text-white/80 text-sm md:text-base italic">
    "Uma impressora parada na sua casa pode ser a prótese que muda a
    vida de alguém na AACD."
  </p>
</section>  

      {/* Seleção de entrada */}
      <section className="flex flex-col items-center pb-16">
        <span className="text-white font-medium mb-4">Como deseja entrar?</span>
        <div className="flex gap-4">
          <button className="flex items-center gap-2 bg-white/10 hover:bg-white/20 transition text-white font-semibold px-6 py-4 rounded-xl">
            Entrar como AACD
          </button>
          <button className="flex items-center gap-2 bg-white/10 hover:bg-white/20 transition text-white font-semibold px-6 py-4 rounded-xl">
            Entrar como Fabricante
          </button>
        </div>
      </section>

      {/* Rodapé */}
      <footer className="text-center text-white/60 text-sm pb-6">
        © {new Date().getFullYear()} MovaHub · Todos os direitos reservados
      </footer>
    </main>
  );
}