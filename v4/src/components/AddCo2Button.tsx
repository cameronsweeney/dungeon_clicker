import { useDispatch } from 'react-redux';
import { addCo2 } from '../app/co2slice.tsx';

const AddCo2Button = () => {
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch(addCo2())}>Add CO2</button>
  );
};

export default AddCo2Button;
