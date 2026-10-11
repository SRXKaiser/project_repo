import { useMemo } from 'react';
import {categoriasDefault} from '../data/explorarContent';


interface FondoCategoriasProps {
  categorias?: string[];
  cantidad?: number;
}

const FondoCategorias = ({ categorias = categoriasDefault, cantidad = 40 }: FondoCategoriasProps) => {
  // Generar posiciones y delays UNA SOLA VEZ (no cambian en cada render)
  const elementos = useMemo(() => {
    const items: {
      id: number;
      texto: string;
      top: number;
      left: number;
      size: number;
      opacity: number;
      delay: number;
      duration: number;
    }[] = [];
    
    for (let i = 0; i < cantidad; i++) {
      const texto = categorias[i % categorias.length];
      items.push({
        id: i,
        texto,
        top: Math.random() * 100,          // 0% - 100%
        left: Math.random() * 100,         // 0% - 100%
        size: 0.7 + Math.random() * 1.3,   // 0.7rem - 2rem
        opacity: 0.15 + Math.random() * 0.5, // 0.15 - 0.65
        delay: Math.random() * 8,           // 0s - 8s
        duration: 8 + Math.random() * 12,   // 8s - 20s
      });
    }
    return items;
  }, [categorias, cantidad]);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
      {elementos.map((el) => (
        <span
          key={el.id}
          className="categoria-flotante font-pixel absolute whitespace-nowrap"
          style={{
            top: `${el.top}%`,
            left: `${el.left}%`,
            fontSize: `${el.size}rem`,
            opacity: el.opacity,            animationDelay: `${el.delay}s`,
            animationDuration: `${el.duration}s`,
            color: 'var(--cafe)',
          }}
        >
          {el.texto}
        </span>
      ))}
    </div>
  );
};

export default FondoCategorias;