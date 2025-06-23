const { build, context } = require('esbuild');
const { glob } = require('glob');
const path = require('path');

async function buildAllComponents(watch = false) {
  try {
    // Find all .tsx files in components directory
    const tsxFiles = await glob('templates/components/**/*.tsx');
    
    if (watch) {
      // Watch mode
      const contexts = await Promise.all(
        tsxFiles.map(async (file) => {
          const componentName = path.basename(file, '.tsx');
          const outfile = `static/${componentName}.js`;
          
          console.log(`Watching ${file} -> ${outfile}`);
          
          const ctx = await context({
            entryPoints: [file],
            bundle: true,
            outfile: outfile,
            format: 'iife',
            target: ['es2020'],
            minify: process.env.NODE_ENV === 'production',
          });
          
          await ctx.watch();
          return ctx;
        })
      );
      
      console.log('Watching all components...');
      // Keep the process running
      process.on('SIGINT', async () => {
        await Promise.all(contexts.map(ctx => ctx.dispose()));
        process.exit(0);
      });
    } else {
      // Build mode
      const builds = tsxFiles.map(async (file) => {
        const componentName = path.basename(file, '.tsx');
        const outfile = `static/${componentName}.js`;
        
        console.log(`Building ${file} -> ${outfile}`);
        
        return build({
          entryPoints: [file],
          bundle: true,
          outfile: outfile,
          format: 'iife',
          target: ['es2020'],
          minify: process.env.NODE_ENV === 'production',
        });
      });
      
      await Promise.all(builds);
      console.log('All components built successfully!');
    }
  } catch (error) {
    console.error('Build failed:', error);
    process.exit(1);
  }
}

// Check if --watch flag is passed
const watch = process.argv.includes('--watch');
buildAllComponents(watch);