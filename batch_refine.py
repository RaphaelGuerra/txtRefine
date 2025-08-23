#!/usr/bin/env python3
"""
Batch Refinement Script for Multiple Files

This script allows you to process multiple transcription files with different models
and settings in batch mode.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
import argparse

def create_batch_config():
    """Create a sample batch configuration file."""
    config = {
        "description": "Configuração para processamento em lote de transcrições",
        "created": datetime.now().isoformat(),
        "batches": [
            {
                "name": "Filosofia - Alta Qualidade",
                "description": "Processa arquivos filosóficos com modelo de alta qualidade",
                "files": ["aula_filosofia.txt", "seminario_escolastica.txt"],
                "model": "mistral:7b",
                "enabled": True
            },
            {
                "name": "Filosofia - Rápido",
                "description": "Processa arquivos filosóficos com modelo rápido",
                "files": ["aula_breve.txt"],
                "model": "gemma:2b",
                "enabled": True
            },
            {
                "name": "Conteúdo Geral",
                "description": "Processa arquivos de conteúdo geral",
                "files": ["palestra_geral.txt"],
                "model": "llama2:7b",
                "enabled": False
            }
        ],
        "global_settings": {
            "input_folder": "input",
            "output_folder": "output",
            "backup_original": True,
            "create_log": True,
            "wait_between_batches": 5
        }
    }
    
    with open("batch_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Arquivo de configuração 'batch_config.json' criado!")
    print("📝 Edite o arquivo conforme suas necessidades e execute novamente.")

def load_batch_config(config_file="batch_config.json"):
    """Load batch configuration from file."""
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração '{config_file}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar arquivo de configuração '{config_file}'.")
        return None

def backup_file(file_path, backup_folder):
    """Create a backup of the original file."""
    if not backup_folder.exists():
        backup_folder.mkdir(parents=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = backup_folder / backup_name
    
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"⚠️  Não foi possível fazer backup de {file_path.name}: {e}")
        return None

def process_batch(batch, input_folder, output_folder, backup_folder=None, create_log=False):
    """Process a single batch of files."""
    print(f"\n🔄 Processando lote: {batch['name']}")
    print(f"📝 Descrição: {batch['description']}")
    print(f"🤖 Modelo: {batch['model']}")
    print(f"📁 Arquivos: {len(batch['files'])}")
    
    if not batch['enabled']:
        print("⏸️  Lote desabilitado, pulando...")
        return True
    
    results = []
    
    for filename in batch['files']:
        input_path = input_folder / filename
        
        if not input_path.exists():
            print(f"⚠️  Arquivo não encontrado: {filename}")
            results.append({
                "file": filename,
                "status": "not_found",
                "error": "Arquivo não encontrado"
            })
            continue
        
        print(f"\n📖 Processando: {filename}")
        
        # Create backup if requested
        backup_path = None
        if backup_folder:
            backup_path = backup_file(input_path, backup_folder)
            if backup_path:
                print(f"💾 Backup criado: {backup_path.name}")
        
        # Process the file
        try:
            output_filename = f"refined_{filename}"
            output_path = output_folder / output_filename
            
            # Import and run refinement
            from src.refine import refine_transcription
            success = refine_transcription(input_path, output_path, batch['model'])
            
            if success:
                print(f"✅ {filename} processado com sucesso")
                results.append({
                    "file": filename,
                    "status": "success",
                    "backup": str(backup_path) if backup_path else None
                })
            else:
                print(f"❌ Falha ao processar {filename}")
                results.append({
                    "file": filename,
                    "status": "failed",
                    "error": "Falha no processamento"
                })
                
        except Exception as e:
            print(f"❌ Erro ao processar {filename}: {e}")
            results.append({
                "file": filename,
                "status": "error",
                "error": str(e)
            })
    
    return results

def main():
    """Main function for batch processing."""
    parser = argparse.ArgumentParser(
        description="Processamento em lote de transcrições com diferentes modelos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 batch_refine.py --create-config    # Create sample configuration file
  python3 batch_refine.py                    # Process all enabled batches
  python3 batch_refine.py --config my_config.json  # Use custom config file
        """
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a sample batch configuration file'
    )
    
    parser.add_argument(
        '--config',
        default='batch_config.json',
        help='Batch configuration file to use (default: batch_config.json)'
    )
    
    args = parser.parse_args()
    
    # Create configuration if requested
    if args.create_config:
        create_batch_config()
        return
    
    # Load configuration
    config = load_batch_config(args.config)
    if not config:
        print("💡 Execute 'python3 batch_refine.py --create-config' para criar um arquivo de configuração.")
        return
    
    print("🚀 Iniciando processamento em lote...")
    print(f"📋 Configuração: {args.config}")
    print(f"📁 Pasta de entrada: {config['global_settings']['input_folder']}")
    print(f"📁 Pasta de saída: {config['global_settings']['output_folder']}")
    
    # Setup folders
    input_folder = Path(config['global_settings']['input_folder'])
    output_folder = Path(config['global_settings']['output_folder'])
    backup_folder = None
    
    if not input_folder.exists():
        print(f"❌ Pasta de entrada não encontrada: {input_folder}")
        return
    
    output_folder.mkdir(exist_ok=True)
    
    if config['global_settings']['backup_original']:
        backup_folder = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"💾 Backups serão salvos em: {backup_folder}")
    
    # Process each batch
    all_results = []
    start_time = datetime.now()
    
    for i, batch in enumerate(config['batches']):
        print(f"\n{'='*60}")
        print(f"📦 Lote {i+1}/{len(config['batches'])}")
        
        results = process_batch(
            batch, 
            input_folder, 
            output_folder, 
            backup_folder,
            config['global_settings']['create_log']
        )
        
        all_results.extend(results)
        
        # Wait between batches if not the last one
        if i < len(config['batches']) - 1 and config['global_settings']['wait_between_batches'] > 0:
            print(f"⏳ Aguardando {config['global_settings']['wait_between_batches']} segundos...")
            time.sleep(config['global_settings']['wait_between_batches'])
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 RESUMO DO PROCESSAMENTO")
    print("=" * 60)
    
    total_files = len(all_results)
    successful = sum(1 for r in all_results if r['status'] == 'success')
    failed = sum(1 for r in all_results if r['status'] in ['failed', 'error'])
    not_found = sum(1 for r in all_results if r['status'] == 'not_found')
    
    print(f"📁 Total de arquivos: {total_files}")
    print(f"✅ Processados com sucesso: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"⚠️  Não encontrados: {not_found}")
    print(f"⏱️  Tempo total: {duration}")
    
    # Save log if requested
    if config['global_settings']['create_log']:
        log_file = output_folder / f"batch_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "config_file": args.config,
            "duration": str(duration),
            "results": all_results
        }
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Log salvo em: {log_file}")
    
    print("\n🎉 Processamento em lote concluído!")

if __name__ == '__main__':
    main()
