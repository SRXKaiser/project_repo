interface BlueBoxProps {
  texto: string;
  align: 'left' | 'right';
}

const BlueBox = ({ texto, align }: BlueBoxProps) => {
  const isLeft = align === 'left';

  return (
    <div
      className={
        isLeft
          ? 'col-span-1 grid grid-cols-subgrid gap-4'
          : 'col-span-2 grid grid-cols-subgrid gap-4'
      }
    >
      <div
        className={`${
          isLeft ? 'col-start-1' : 'col-start-2'
        } bg-[var(--celeste)] p-10 ml-15 mr-15 text-center font-semibold text-xl`}
      >
        {texto}
      </div>
    </div>
  );
};

export default BlueBox;