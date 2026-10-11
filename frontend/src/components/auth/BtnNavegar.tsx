interface BtnNavegarProps {
  pasoActual: number;
  pasoTotal: number;
  onAtras: () => void;
  onSiguiente: () => void;
  textoFinal?: string;   // por defecto "CREAR CUENTA"
}

const BtnNavegar = ({
  pasoActual,
  pasoTotal,
  onAtras,
  onSiguiente,
  textoFinal = 'CREAR CUENTA',
}: BtnNavegarProps) => {
  return (
    <div className="flex flex-row gap-2 w-72 mt-4">
      {pasoActual > 1 && (
        <button
          type="button"
          onClick={onAtras}
          className="btn btn-ng flex-1 rounded-xl
                     border-2 border-[var(--rosita)]
                     text-[var(--rosita)] font-semibold
                     hover:bg-[var(--rosita)]/10 transition"
        >
          <span className="btn-tapa">← REGRESAR</span>
        </button>
      )}

      {pasoActual < pasoTotal ? (
        <button
          type="button"
          onClick={onSiguiente}
          className="btn btn-ng flex-1"
        >
          <span className="btn-tapa">SIGUIENTE →</span>
        </button>
      ) : (
        <button type="submit" className="btn btn-ng flex-1">
          <span className="btn-tapa">{textoFinal}</span>
        </button>
      )}
    </div>
  );
};

export default BtnNavegar;