export default function ProgressComponent(
    {
        i,
        len
    }:
    {
        i: number;
        len: number
    }
)
{
    return (
        <div>
            {`${i}/${len}`}
        </div>
    );
}
