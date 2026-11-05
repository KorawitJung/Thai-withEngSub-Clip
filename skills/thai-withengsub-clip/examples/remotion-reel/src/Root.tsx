import {Composition} from 'remotion';
import {Cover, Reel, clips, coverIds, durationFrames} from './Reel';

export const Root = () => (
	<>
		{clips.map((c) => (
			<Composition key={c.id} id={c.id} component={Reel} fps={30} width={1080} height={1920} durationInFrames={durationFrames(c)} defaultProps={{clipId: c.id}} />
		))}
		{coverIds.map((id) => (
			<Composition key={id} id={id} component={Cover} fps={30} width={1080} height={1920} durationInFrames={150} defaultProps={{id}} />
		))}
	</>
);
